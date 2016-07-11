<template>
    <vs-form v-on:submit.prevent="submit" :errors="errors">
        <vs-form-input
            :model.sync="username"
            type="text"
            label="用户名"
            description="请输入您的用户名（注意不是昵称）"
            name="username"
            size="md">        
        </vs-form-input>
        <vs-form-input
            :model.sync="password"
            type="password"
            label="密码"
            name="password"
            description="请输入密码"
            size="md">        
        </vs-form-input>
        <div class="form-group row">
            <div class="col-md-12">
                <button type="submit" class="btn btn-success" :disabled="loading">登录</button>
            </div>
        </div>
    </vs-form>
</template>

<script>
    export default {
        data: () => ({
            username: "",
            password: "",
            errors: {},
            loading: false
        }),
        methods: {
            submit (e) {
                let resource = this.$resource('users', {}, {
                    login: {
                        method: 'POST',
                        url: 'users/login/'
                    }
                })

                resource.login({}, this.$data).then((res) => {
                    this.$root.$emit('logined', res.data)
                    this.$root.$broadcast('logined', res.data)
                })
            }
        }
    }
</script>