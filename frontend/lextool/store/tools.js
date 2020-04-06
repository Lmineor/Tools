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
                    }
                },
            ]
        },
        {
            title: '嗑盐工具',
            icon: 'layers-outline',
            list: [
                {
                    name: 'Sci-Hub',
                    path: '/screen_record',
                    head: {
                        keywords: ['屏幕录制', '在线录屏'],
                        description: '在网页上完成录屏'
                    }
                },
                {
                    name: 'Sci',
                    path: 'https://www.baidu.com',
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
                {
                    name: '网站设置',
                    path: '/setting'
                },
                {
                    name: '工具隐藏',
                    path: '/hide_tool'
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
