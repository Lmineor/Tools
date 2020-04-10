export const state = () => {
    const tools = [
        {
            title: '热点相关',
            icon: 'options-2-outline',
            list: [
                {
                    name: '重启的武汉',
                    path: 'https://www.bilibili.com/video/BV18i4y187BB',
                    head: {
                        keywords: ['武汉', '肺炎'],
                        description: '武汉重启的介绍'
                    }
                },
                {
                    name: '新冠肺炎',
                    path: 'https://ncov.dxy.cn/ncovh5/view/pneumonia',
                    head: {
                        keywords: ['武汉', '肺炎'],
                        description: '武汉重启的介绍'
                    }
                },
            ]
        },
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
                    }
                },
                {
                    name: 'Leetcode',
                    path: 'https://leetcode-cn.com/',
                    head: {
                        keywords: ['刷题', '技能get'],
                        description: 'leetcode'
                    }
                },
                {
                    name: 'Markdown',
                    path: '/markdown',
                    head: {
                        keywords: ['Markdown'],
                        description: 'Markdown'
                    }
                },
            ]
        },
        {
            title: '嗑盐工具',
            icon: 'layers-outline',
            list: [
                {
                    name: 'Sci-Hub可用网址',
                    path: 'http://www.howsci.com/sci-hub-alternative.html',
                    head: {
                        keywords: ['屏幕录制', '在线录屏'],
                        description: '在网页上完成录屏'
                    }
                },
                {
                    name: '科研动力',
                    path: 'http://www.howsci.com/',
                    head: {
                        keywords: ['屏幕录制', '在线录屏'],
                        description: '在网页上完成录屏'
                    }
                },
            ]
        },
        {
            title: '网站相关',
            icon: 'settings-2-outline',
            list: [
                // {
                //     name: '网站设置',
                //     path: '/setting'
                // },
                // {
                //     name: '工具隐藏',
                //     path: '/hide_tool'
                // },
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
