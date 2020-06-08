export const state = () => {
    const tools = [
        {
            title: '编程开发',
            icon: 'code-outline',
            list: [
                {
                    name: '短链生成',
                    path: '/shorturl',
                    head: {
                        keywords: ['url', '短链'],
                        description: '短链生成工具'
                    },
                    hot:''//debug new recommend
                },
                {
                    name: '短链还原',
                    path: '/originurl',
                    head: {
                        keywords: ['还原', '短链'],
                        description: '短链还原工具'
                    },
                    hot:'new'//debug new recommend
                },
                {
                    name: 'Leetcode',
                    path: 'https://leetcode-cn.com/',
                    head: {
                        keywords: ['刷题', '技能get'],
                        description: 'leetcode'
                    },
                    hot:''//debug new recommend
                },
                {
                    name: 'Markdown',
                    path: '/markdown',
                    head: {
                        keywords: ['Markdown'],
                        description: 'Markdown'
                    },
                    hot:'', //debug new recommend
                },
            ]
        },
        {
            title: '学习工具',
            icon: 'layers-outline',
            list: [
                {
                    name: '背背单词',
                    path: '/words',
                    head: {
                        keywords: ['单词'],
                        description: '背背单词'
                    },
                    hot:'new'//debug new recommend
                },
                {
                    name: 'Sci-Hub可用网址',
                    path: '/sci',
                    head: {
                        keywords: ['嗑盐', '嗑盐'],
                        description: 'Sci-Hub可用网址'
                    },
                    hot:''//debug new recommend
                },
                {
                    name: '科研动力',
                    path: 'http://www.howsci.com/',
                    head: {
                        keywords: ['嗑盐', '动力'],
                        description: '科研动力'
                    },
                    hot:''//debug new recommend
                },
            ]
        },
        {
            title: '中国文学',
            icon: 'book-outline',
            list: [
                {
                    name: '诗歌',
                    path: '/poem',
                    head: {
                        keywords: ['唐诗', '宋诗'],
                        description: '唐诗宋词元曲'
                    },
                    hot:'recommend'//debug new recommend
                },
                {
                    name: '论语',
                    path: '/lunyu',
                    head: {
                        keywords: ['论语', '子曰'],
                        description: '论语'
                    },
                    hot:'new'//debug new recommend
                },
                {
                    name: '宋词',
                    path: '/songci',
                    head: {
                        keywords: ['宋词'],
                        description: '宋词'
                    },
                    hot:'new'//debug new recommend
                },
                {
                    name: '诗经',
                    path: '/shijing',
                    head: {
                        keywords: ['诗经', '风'],
                        description: '诗经'
                    },
                    hot:'new'//debug new recommend
                },
            ]
        },
        // {
        //     title: '为人民服务',
        //     icon: 'briefcase-outline',
        //     list: [
        //         {
        //             name: '号码归属地',
        //             path: '/location'
        //         }
        //     ]
        // },
        {
            title: '热点相关',
            icon: 'options-2-outline',
            list: [
                {
                    name: '新冠肺炎',
                    path: 'https://ncov.dxy.cn/ncovh5/view/pneumonia',
                    head: {
                        keywords: ['武汉', '肺炎'],
                        description: '武汉重启的介绍'
                    },
                    hot:''//debug new recommend
                },
                {
                    name: '百度热榜',
                    path: 'http://top.baidu.com/?fr=mhd_card',
                    head: {
                        keywords: ['百度热榜', '百度热榜'],
                        description: '百度热榜'
                    },
                    hot:'new'//debug new recommend
                },
            ]
        },
        {
            title: '其他工具',
            icon: 'heart-outline',
            list: [
                {
                    name: '便签',
                    path: '/memo',
                    head: {
                        keywords: ['memo'],
                        description: 'memo'
                    },
                    hot:'new', //debug new recommend
                },
                // {
                // name: '号码归属地',
                // path: '/location',
                // hot:'new', //debug new recommend
                // },
            ]
        },
        {
            title: '网站相关',
            icon: 'settings-2-outline',
            list: [
                {
                    name: '个人信息',
                    path: '/userinfo'
                },
                {
                    name: '帮助',
                    path: '/help'
                },
                {
                    name: '友情链接',
                    path: '/links'
                }
            ]
        }
    ];

    tools.forEach(i => {
        i.list.forEach(tool => {
            let head = {
                meta: []
            };
            if (!tool.head) {
                tool.head = head;
            }

            head.title = `${tool.head.title ? tool.head.title : tool.name} - ${
                process.env.title
            }`;
            if (tool.head.other) {
                head.meta = head.meta.concat(tool.head.other);
            }
            if (tool.head.keywords) {
                tool.head.keywords = tool.head.keywords.concat([
                    'Lexools',
                    '在线工具'
                ]);
                head.meta.push({
                    hid: 'keywords',
                    keywords: tool.head.keywords.join(',')
                });
            }
            if (tool.head.description) {
                head.meta.push({
                    hid: 'description',
                    description: tool.head.description
                });
            }
            tool.head = head;
            const pinyin = process.env.pinyin;
            if (pinyin) {
                tool.pinyin = pinyin[tool.name];
            }
        });
    });
    return tools;
};
