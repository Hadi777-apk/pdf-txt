exports.handler = async (event, context) => {
  const { path = '' } = event.queryStringParameters || {};
  const targetUrl = `http://8.153.206.100${path ? '/' + path : ''}`;
  
  try {
    const response = await fetch(targetUrl, {
      method: event.httpMethod,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      }
    });
    
    let content = await response.text();
    const contentType = response.headers.get('content-type') || '';
    
    // 如果是 HTML 内容，修复相对路径
    if (contentType.includes('text/html')) {
      content = content.replace(/href="(?!http|\/\/|#)/g, 'href="/.netlify/functions/proxy?path=');
      content = content.replace(/src="(?!http|\/\/|data:)/g, 'src="/.netlify/functions/proxy?path=');
      content = content.replace(/url\((?!http|\/\/|data:)/g, 'url(/.netlify/functions/proxy?path=');
    }
    
    return {
      statusCode: response.status,
      headers: {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      },
      body: content
    };
    
  } catch (error) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        error: 'Failed to fetch content',
        message: error.message
      })
    };
  }
};