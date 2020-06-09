<template>
    <div class="words">
        <nya-container :title="title">
            <div v-show="!showInfo">
                <table class="nya-table">
                    <tr>
                        <th>单词</th>
                        <th>词义</th>
                        <th>英文详解</th>
                    </tr>
                    <tr v-for="(item, index) in words" :key="index">
                        <td>{{ item.word }}</td>
                        <td class="translation">{{ item.translation }}</td>
                        <td class="view-deep" @click="searchWord(item.word)">
                            英文详解
                        </td>
                    </tr>
                </table>
            </div>
            <!-- <Table stripe :columns="columns" :data="words"></Table> -->
            <div v-show="showInfo" class="show-info">
                <div class="back nya-btn" @click="showInfo = false">
                    <i class="eva eva-arrow-back-outline"></i>
                    <span>返回</span>
                </div>

            </div>
        </nya-container>
    </div>
</template>

<script>
import envs from '../env'

export default {
    name: 'ShortUrl',
    head() {
        return{
            title: this.title
        }
    },
    data() {
        return {
            title: '每日英语',
            loading: true,
            showInfo: false,
            columns: [
                    {
                        title: '单词',
                        key: 'word'
                    },
                    {
                        title: '词义',
                        key: 'translation'
                    }
                ],
            words: [],
        };
    },
    mounted (){
        this.getWords()
    },
    methods: {
        getWords() {
            this.$store.commit('SET_STORE', {
                key: 'globalLoading',
                value: true
            });
            this.$axios
                .get(envs.apiUrl + '/words/daily',)
                .then(re => {
                    this.words = re.data.words;
                    this.$store.commit('SET_STORE', {
                        key: 'globalLoading',
                        value: false
                    });
                })
                .catch(err => {
                    this.$store.commit('SET_STORE', {
                        key: 'globalLoading',
                        value: false
                    });
                    this.$swal({
                        toast: true,
                        position: 'top-end',
                        type: 'error',
                        title: 'error' + err,
                        timer: 3000,
                    });
                });
            this.loading = false;
        },
        searchWord(){
            this.showInfo = true;

        }
    }
};
</script>

<style lang="scss">
.words {
    table {
        table-layout: auto;
        width: 100%;
        .translation{
            max-width: 500px;
        }
        .view-deep {
            cursor: pointer;
        }
    }
    .show-info {
        ul {
            margin: 0;
            padding: 0;
            li {
                list-style: none;
            }
        }
        ul.info {
            margin: 15px 0;
            li {
                line-height: 1.3;
                .title {
                    font-weight: bold;
                }
            }
        }
        .view-cdn-list {
            li {
                cursor: pointer;
            }
        }
    }
    .cdnjs_modal {
        padding: 15px;
        border-radius: 5px;
        background-color: var(--t2);
        max-width: 100%;
        font-size: 18px;
        .title {
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
            padding-bottom: 15px;
            border-bottom: 1px solid #dad9d9;
            .start-speed {
                display: inline-block;
                font-size: 14px;
                padding: 2px 8px;
                border: 1px solid var(--border-color);
                margin-left: 5px;
                cursor: pointer;
            }
        }
        table {
            .cdnlink {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                max-width: 250px;
            }
        }
    }
    // .fullversion_modal {
    // }
}
</style>