// import pinyin from './pinyin';

export default {
    title: 'Lex吐司',
    domain:
        process.env.NODE_ENV === 'development'
            ? 'https://www.lex666.online/tools'
            : 'lex666.online/',
    description: '一个轻量的工具集合',
    url:
        process.env.NODE_ENV === 'development'
            ? 'http://dev.lex666.onlines/tools/'
            : 'https://www.lex666.onlines/tools/',
    apiUrl:
        process.env.NODE_ENV === 'development'
            ? 'http://dev.miku.tool:3001'
            : 'https://api.lex666.onlines',
    // pinyin: pinyin,
    development: process.env.NODE_ENV === 'development',
    axios:
        process.env.NODE_ENV === 'development'
            ? 'http://127.0.0.1:5000/shorten'
            : 'https://api.lex666.onlines'
};
