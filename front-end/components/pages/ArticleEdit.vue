<template>
    <div>
        <form @submit.prevent="submit">
            <vs-form-input
                :model.sync="title"
                type="text"
                name='title'
                placeholder="标题">
            </vs-form-input>
            <editor name="content" editor-id="articles-editor" :model.sync="content"></editor>
            <vs-form-button>发布</vs-form-button>
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
            content: ""
        }),
        ready () {
            console.log(this.$children)
        },
        methods: {
            submit () {
                this.$http.post('/api/articles/', this.$data)
            }
        }
    }
</script>