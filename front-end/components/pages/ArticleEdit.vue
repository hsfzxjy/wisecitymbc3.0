<template>
    <div>
        <form @submit.prevent="submit">
            <vs-form-input
                :model.sync="title"
                type="text"
                name='title'
                :state='errors.title | state'
                placeholder="标题">
            </vs-form-input>
            <editor name="content" editor-id="articles-editor" :model.sync="content"></editor>
            <vs-form-button :disabled="loading">发布</vs-form-button>
        </form>
    </div>
</template>

<script>
    import Editor from '../Editor.vue'

    export default {
        components: {
            Editor
        },
        data: () => ({
            title: "",
            content: "",
            errors: {},
            loading: false
        }),
        methods: {
            submit () {
                this.loading = true

                this.$http.post('/api/articles/', this.$data)
                    .then((res) => {

                    }, (res) => {
                        if (res.status === 400) {
                            this.errors = res.data
                        }
                    }).then(() => {
                        this.loading = false;
                    })
            }
        }
    }
</script>