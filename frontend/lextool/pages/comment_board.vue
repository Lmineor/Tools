<template>
  <div>
    <nya-container :title=title>
      <div class="comment">
        <div style="margin-bottom: 20px;padding-bottom: 10px">
          <span style="font-weight: bold;font-size: 19px">审核通过的将会在这里显示</span>
          <div class="nya-btn" id="register" @click="show_drawer = true" style="float: right">吐个槽</div>
          <Drawer
              title="吐槽中心"
              v-model="show_drawer"
              width="400"
              :mask-closable="true"
              :styles="styles"
          >
            <Form :model="formValidate" :rules="ruleValidate" ref="formData">
                <Row :gutter="32">
                    <Col span="12">
                        <FormItem label="邮箱" label-position="top" prop="mail" >
                            <Input v-model="formValidate.mail" placeholder="请输入邮箱"/>
                        </FormItem>
                    </Col>

                </Row>
                <Row :gutter="32">
                    <Col span="12">
                        <FormItem label="吐槽类型" label-position="top" prop="type" >
                            <Select v-model="formValidate.type" placeholder="类型" >
                                <Option value="suggestion">功能建议</Option>
                                <Option value="question">问题反馈</Option>
                                <Option value="other">其他</Option>
                            </Select>
                        </FormItem>
                    </Col>
                </Row>
                <Row>
                  <Col span="12">
                      <FormItem label="时间" label-position="top">
                        <DatePicker v-model="formValidate.date" :disabled=true style="display: block" placement="bottom-end"></DatePicker>
                      </FormItem>
                  </Col>
                </Row>
                <FormItem label="详细说说" label-position="top" prop="content">
                    <Input type="textarea" v-model="formValidate.content" :rows="4" placeholder="展开说说看" maxlength="255" show-word-limit/>
                </FormItem>
            </Form>
            <div class="demo-drawer-footer">
              <div class="nya-btn" @click="make_complaints" style="margin-right: 8px">确定</div>
              <div class="nya-btn" @click="show_drawer = false">取消</div>
            </div>
        </Drawer>
        </div>
        <template v-for="comment in comments">
          <Card class="help-card">
            <p slot="title" style="font-weight: bold;font-size: 20px">
              <Icon type="ios-alert-outline" />
                {{types[comment.comment_type]}}
            </p>
            <span slot="extra">{{comment.create_at}}</span>
            <ul>
              <span style="font-size: 17px">
                <Icon type="md-book" />
                {{ comment.content }}
              </span>
            </ul>
          </Card>
        </template>
      </div>
    </nya-container>
    <nya-container title="说明">
        <ul class="nya-list">
            <li>若有特殊原因未能提交成功，可以直接联系我邮箱：<a href="mailto:luohai2233@163.com">luohai2233@163.com</a></li>
        </ul>
    </nya-container>
  </div>
</template>

<script>
import envs from '../env'



export default {
  name: 'help',
  data() {
    return {
      title: '吐槽中心',
      show_drawer: false,
      styles: {
        height: 'calc(100% - 55px)',
        overflow: 'auto',
        paddingBottom: '53px',
        position: 'static'
      },
      ruleValidate: {
        type: [
          {required: true, message: '请选择要吐槽的类型', trigger: 'change'}
        ],
        mail: [
          {required: true, message: '邮箱不能为空', trigger: 'blur'},
          {type: 'email', message: '邮箱格式不正确', trigger: 'blur'}
        ],
        content: [
          {required: true, message: '内容不能为空', trigger: 'change'}
        ]
      },
      formValidate: {
        mail: '',
        type: 'other',
        date: '',
        content: ''
      },
      comments: [],
      types:{'suggestion': '功能建议', 'question':'问题反馈', 'other':'其他'}
    }
  },
  mounted() {
    this.get_complaints();
    this.getTime();
    setInterval(() => {
      this.getTime();
    }, 1000 * 60)
  },
  methods: {
    make_complaints() {
      this.$axios
        .post(
          envs.apiUrl + '/helps/comment',
          {
            mail: this.formValidate.mail,
            type: this.formValidate.type,
            content: this.formValidate.content,
            date: this.formValidate.date
          },
        )
        .then(re => {
          let code = re.data.code;
          if (code === 200) {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'success',
              title: '反馈成功',
              timer: 1000,
            });
            setInterval(() => {
            }, 1000 * 3);
            this.formValidate.mail = '';
            this.formValidate.type = '';
            this.getTime();
            this.formValidate.content = '';
            this.show_drawer = false;
          } else {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: re.data.msg,
              timer: 3000,
            });
          }
        })
        .catch(err => {
          this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: err,
            timer: 3000,
          });
          this.loading_content = false;
        });
    },
    get_complaints() {
      this.$store.commit('SET_STORE', {
        key: 'globalLoading',
        value: true
      });
      this.$axios
        .get(envs.apiUrl + '/helps/comment')
        .then(re => {
          this.comments = re.data.data;
          this.$store.commit('SET_STORE', {
            key: 'globalLoading',
            value: false
          });
        })
        .catch(err => {
          this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: err,
            timer: 3000,
          });
          this.$store.commit('SET_STORE', {
            key: 'globalLoading',
            value: false
          });
        });
    },
    getTime: function () {
      let yy = new Date().getFullYear();
      let mm = new Date().getMonth() + 1;
      let dd = new Date().getDate();
      this.formValidate.date = yy + '-' + mm + '-' + dd;
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .comment {
    display: table;
    width: 100%;
    .demo-drawer-footer{
        width: 100%;
        position: absolute;
        bottom: 0;
        left: 0;
        border-top: 1px solid #e8e8e8;
        padding: 10px 16px;
        text-align: right;
        background: #fff;
    }
    .help-card {
      margin-bottom: 10px;
      position: relative;
    }
  }
</style>
