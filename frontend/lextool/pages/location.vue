<template>
    <div class="location">
        <nya-container title="号码归属地查询">
            <nya-input
                v-model.trim="mobile"
                label="请输入要查询的号码"
                placeholder="16666888866"
                autocomplete="off"
                autofocus
                fullwidth
            />
            <div class="nya-btn" @click="getLocation">
                查询
            </div>
        </nya-container>
        <nya-container v-if="prov" title="结果">
            <div class="show-res">
                <li>{{mobile}}</li>
                <li>{{type}}</li>
                <li>{{prov}}</li>
                <li>{{city}}</li>
            </div>
        </nya-container>

    </div>
</template>

<script>
import envs from '../env'
import {validMobile} from '@/utils/validate'

export default {
    name: 'location',
    head() {
        return {
            title: '号码归属地查询'
        };
    },
    data() {
        return {
            mobile:'',
            city:'',
            prov:'',
            type:''
        };
    },
    methods: {
        getLocation() {
            if (!validMobile(this.mobile)){
                this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'error',
                    title: '手机号码格式有误',
                    timer: 1500,
                });
                return;
            }
            this.$axios.credentials = true;
            this.$axios
                .get(
                    'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_name=guishudi&query=' + this.mobile, 
                    {
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                        },
                        auth: false
                    }
                    )
                .then(re => {
                    let data = re.data.data
                    if(!data){
                        this.$swal({
                            toast: true,
                            position: 'top-end',
                            type: 'error',
                            title: '好像还查不到这个号码呀！',
                            timer: 1500,
                        });
                    }
                    this.type = data[0].type;
                    this.prov = data[0].prov;
                    this.city = data[0].city;
                })
                .catch(err => {
                    this.$swal({
                        toast: true,
                        position: 'top-end',
                        type: 'error',
                        title: '出了点错误，请稍后再试~',
                        timer: 1500,
                    });
                });
        },
    }
};
</script>

<style lang="scss">
.location {
    .nya-btn {
        margin-top: 15px;
    }
}
</style>