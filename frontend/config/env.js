const configs = {
  // 测试环境
  test: {
    API_SERVER: 'http://127.0.0.1:8080',
  },

  // dev环境
  dev: {
    API_SERVER: 'http://192.168.23.160:8089',
  },

  // 线上环境
  prod: {
    API_SERVER: 'http://127.0.0.1:8888',
  },

};

const APP_ENV = process.env.APP_ENV;
console.log(APP_ENV, configs[APP_ENV].API_SERVER, '------APP_ENV-----');

export default configs;
