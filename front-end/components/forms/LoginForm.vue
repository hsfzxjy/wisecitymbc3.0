<template>
    <form v-on:submit.prevent="submit">
        <vs-form-input
            :model.sync="username"
            type="text"
            label="用户名"
            description="请输入您的用户名（注意不是昵称）"
            :state="errors | state"
            size="md">        
        </vs-form-input>
        <vs-form-input
            :model.sync="password"
            type="password"
            label="密码"
            :state="errors | state"
            description="请输入密码"
            size="md">        
        </vs-form-input>
        <div class="form-group row">
            <div class="col-md-12">
                <button type="submit" class="btn btn-success" :disabled="loading">Sign in</button>
            </div>
        </div>
    </form>
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

                this.loading = true

                resource.login({}, this.$data).then((res) => {
                    this.$dispatch('logined', res.data)
                }, (res) => {
                    if (res.status === 400) {
                        this.errors = res.data
                    }
                }).then(() => {
                    this.loading = false
                })
            }
        }
    }
</script>