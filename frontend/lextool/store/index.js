import _ from 'lodash';
import env from '../env';
import Vuex from 'vuex'
const cookieparser = process.server ? require('cookie-parser') : undefined

export const state = () => ({
    dark: false,
    noticeId: false,
    inFrames: false,
    currentTool: null,
    disabledMouseWheel: false,
    ads: true,
    loaded: false,
    setting: {
        animations: true,
        hide: [],
        favorites: [],
        hideCategory: false,
        hidePay: false,
        hideNotice: false,
        css: '',
        js: '',
        inNewTab: null,
        bg: {
            type: 'none',  //fix or random  frontend\lextool\static\image\12.jpg
            file_path: '',
            blur: 4,
            opacity: 50,
            transparentEl: true
        }
    },
    globalLoading: false,
    welcome: true,
    isMobile: {},
    env: env,
    syncTime: 0,
});

const disabledMouseWheel = e => e.stopPropagation();
export const mutations = {
    SET_STORE(state, n) {
        if (_.isArray(n.value)) {
            n.value = Array.from(n.value);
        }
        if (_.isObject(n.value)) {
            n.value = _.chain(n.value)
                .assign()
                .value();
        }
        state = _.chain(state)
            .set(n.key, n.value)
            .value();
    },
    loadingComponent(state, n) {
        state.globalLoading = n;
    },
    switchTheme(state, n) {
        if (n !== undefined) {
            state.dark = n;
        } else {
            state.dark = !state.dark;
        }
    },
    disabledMouseWheel(state, type) {
        if (type) {
            document.addEventListener('wheel', disabledMouseWheel, {
                passive: true
            });
        } else {
            document.removeEventListener('wheel', disabledMouseWheel, {
                passive: true
            });
        }
        state.disabledMouseWheel = type;
    }
};



// const cookieParser = require('cookie-parser');
// app.use(cookieParser('123456')); //使用cookie中间件，传入签名123456进行加密
// res.cookies('key','value',option) //设置cookie,需要设置signed签名
export const actions = {
    // nuxtServerInit is called by Nuxt.js before server-rendering every page
    nuxtServerInit({ commit }, { req }) {
        console.log('nuxt init')
        console.log(req.headers.cookie)
        let auth = null
        if (req.headers.cookie) {
          const parsed = cookieparser.parse(req.headers.cookie)
          try {
            auth = JSON.parse(parsed.auth)
          } catch (err) {
            // No valid cookie found
          }
          commit('SET_AUTH', auth)
        }
    },
    /**
       * 获取用户信息
       * @param state
       * @param commit
       * @returns {Promise<void>}
       */
      async getUserInfo({state, commit}) {
        if (state.userInfo) {
          return
        }
        const {data} = await env.axios
        // const {data} = await Service.userInfo.request(state.auth)
        commit('SET_USER_IFO', data)
      },
}