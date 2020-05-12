// import pinyin from './pinyin';

export default {
    title: 'Lex吐司',
    domain:
        process.env.NODE_ENV === 'development'
            ? 'https://www.lex666.online'
            : 'https://www.lex666.online/',
    description: '一个轻量的工具集合',
    url:
        process.env.NODE_ENV === 'development'
            ? 'http://tools.lex666.online'
            : 'http://tools.lex666.online',
    apiUrl:
        process.env.NODE_ENV === 'development'
            ? 'http://localhost:5000'
            : 'http://api.lex666.online',
    // pinyin: pinyin,
    development: process.env.NODE_ENV === 'development',
    axios:
        process.env.NODE_ENV === 'development'
            ? 'http://127.0.0.1:5000'
            : 'https://www.lex666.online'
};
