// Code loosely based on https://antoinevastel.com/crawler/2018/09/20/parallel-crawler-puppeteer.html
const puppeteer = require('puppeteer');
const {readFile,writeFile,mkdir,readdir,stat} = require('fs').promises;
const isFile = path=>stat(path).then(s=>s.isFile());
const isDirectory = path=>stat(path).then(s=>s.isDirectory());
const ensureDir = path=>mkdir(path,{recursive:true});

const crawl = async () => {
  const INDEX = './data/scrape_index.json'; // assumes shape like {resolved:{},to_visit:['/'],errors:[]}
  const index = require(INDEX);

  // retry errors
  // console.log(index.errors);
  // index.to_visit.push(...index.errors);
  // index.errors=[];

  if (index.to_visit.length===0){console.log('scrape.js: No nodes to crawl.');return;}

  // key is just url with ROOT_URL removed to decrease index size
  // postStoragePath is key replacing "/" with "_"
  const keyToPostStoragePath = key=>`${__dirname}/data/posts/${key.replace(/\//g,'_')}.txt`;
  const POST_REGEX=/^\/\d+\/\d+\/[^/]+\/$/;
  const MONTH_REGEX=/^\/\d+\/\d+\/.*$/;
  const SITE_REGEX=/^\/$/;

  const attempt_resolve_node = (page,node)=>{
    if(POST_REGEX.test(node.key)){
      return page.$eval('.pf-content',content=>content.innerText)
      .catch(e=>{console.warn(`unable to get innerText for ${node.key}`);throw e;})// 404 case
      .then(post_content=>{
        return writeFile(keyToPostStoragePath(node.key),post_content)
        .then(()=>[])// leaf node - no other nodes to crawl
        .catch(e=>{console.warn(`unable to write file: ${keyToPostStoragePath(node.key)}`);throw e;})
      });
    }

    if(MONTH_REGEX.test(node.key)){
      return page.evaluate(_=>{
        // using location.origin in a couple places since ROOT_URL is undefined in browser context
        // puppeteer has a way to make it defined, but this works for now.
        const author_regex=/^.*?author\/(.*?)\/$/;
        const [na,year,month]=location.pathname.split('/');

        const posts = Array.from(document.querySelectorAll('.post')).map(post=>{
          const day = (post.querySelector(`.post-date .day`)||{innerText:""}).innerText
          const author = (post.querySelector(`.byline a`)||{href:""}).href.replace(author_regex,'$1');
          const title = (post.querySelector(`.post-title-link`)||{title:""}).title;
          const key = (post.querySelector(`.post-title-link`)||{href:""}).href.replace(location.origin,'')
          return {day,year,month,author,title,key};
        });

        // handle paginated month post lists
        const nextPosts = document.querySelector('.nextpostslink');
        // nextPosts is null on the last pagination page
        if (nextPosts!==null) posts.push({key:nextPosts.href.replace(location.origin,'')});
        return posts;
      })
      .catch(e=>{console.warn(`unable to get month index value ${node.key}`);throw e;})
    }

    if(SITE_REGEX.test(node.key)){
      return page.$$eval('#archives-dropdown-3 > option',os=>(
        os.filter(o=>!!o.value).map(o=>({key:o.value.replace(location.origin,'')}))
      ))
      .catch(e=>{console.warn(`unable to get index values for ${node.key}`);throw e;})
    }

    throw new Error('error unrecognized url pattern: '+node.key);
  }


  
  const ROOT_URL = 'https://ritholtz.com';
  const startDate = new Date().getTime();
  const MAX_BROWSERS = 1;
  const MAX_PAGES_PER_BROWSER = 2;
  const USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3239.108 Safari/537.36';
  const promisesBrowsers = [];
  let indexThrottle = -1;
  for (let numBrowser= 0; numBrowser < MAX_BROWSERS; numBrowser++) {
    promisesBrowsers.push(new Promise(async (resBrowser) => {
      const browser = await puppeteer.launch({/*slowMo:2000,*/devtools:false,ignoreHTTPSErrors:true });
      const promisesPages = [];
      // note to self: could improve in speed and memory with a queue of reused pages
      // looping over to_visit, waiting for page ready - but this worked in a few hours with 38k pages
      for (let numPage = 0; numPage < MAX_PAGES_PER_BROWSER; numPage++ ) {
        promisesPages.push(new Promise(async(resPage) => {
          while(index.to_visit.length > 0) {
            const node = index.to_visit.pop();
            if (index.resolved[node.key]){console.log(`${node.key} already visited. ignoring.`);continue;}
            let page = await browser.newPage();

            try{
              console.log(`Visiting : ${node.key}`);
              await page.setUserAgent(USER_AGENT);
              await page.goto(ROOT_URL+node.key,{waitUntil:'domcontentloaded',timeout:30000});
              let edges = await attempt_resolve_node(page,node);
              edges=edges.filter(n=>index.resolved[n.key]===undefined);
              if (edges.length) index.to_visit = [...edges,...index.to_visit];
              index.resolved[node.key]=node;
            } catch(err) {
              console.log(`An error occured on: ${node.key}... re-pushing on to_visit`);
              console.error(err);
              node.error = err.message;
              index.errors.push(node);
            } finally {
              if (++indexThrottle % 30){
                await writeFile(INDEX,JSON.stringify(index));
              }
              await page.close();
            }
          }
          resPage();
        }));
      }

      await Promise.all(promisesPages);
      await writeFile(INDEX,JSON.stringify(index));
      await browser.close();
      resBrowser();
    }));
  }

  await Promise.all(promisesBrowsers);
  console.log(`Time elapsed ${Math.round((new Date().getTime() - startDate) / 1000)} s`);
};

crawl();
