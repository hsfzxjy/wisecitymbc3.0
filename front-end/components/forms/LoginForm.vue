<template>
    <form v-on:submit.prevent="submit">
        <vs-form-input
            :model.sync="username"
            type="text"
            label="用户名"
            description="请输入您的用户名（注意不是昵称）"
            :state="unstate"
            size="md">        
        </vs-form-input>
        <vs-form-input
            :model.sync="password"
            type="text"
            label="密码"
            description="请输入密码"
            size="md">        
        </vs-form-input>
        <div class="form-group row">
            <div class="col-md-12">
                <button type="submit" class="btn btn-success">Sign in</button>
            </div>
        </div>
    </form>
</template>

<script>
    import vsBase from "vuestrap-base-components"

    export default {
        components: {
            'vs-form-input': vsBase.formInput
        },
        data: () => ({
            username: "",
            password: "",
            unstate: ""
        }),
        methods: {
            submit (e) {
                e.preventDefault()

                let resource = this.$resource('users', {}, {
                    login: {
                        method: 'POST',
                        url: 'users/login/'
                    }
                })
                console.log(this.$data)
                resource.login({}, this.$data)
            }
        }
    }
</script>