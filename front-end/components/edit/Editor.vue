<template>
    <form @submit.prevent="submit" class="col-md-9">
        <slot name="fields-before"></slot>
        <ck-editor editor-id="{{name}}-editor" :model.sync="model.content"></ck-editor>
        <slot name="fields-after"></slot>
    </form>
    <div class="col-md-3">
        <uploader 
            browse-button-id="{{name}}-editor-upload"
            :files="model.attachments">
            <vs-buttons id="{{name}}-editor-upload" variant="primary">添加文件</vs-buttons>
        </uploader>
        <vs-buttons :disabled="loading" @click="submit">
            <slot name="submit-name">发布</slot>
        </vs-buttons>
        <vs-list-group>
            <vs-list-group-item
                v-for="file in model.attachments">
            {{file.file_name}}
            </vs-list-group-item>
        </vs-list-group>
    </div>
</template>

<script>
    import _ from 'lodash'
    import CkEditor from 'components/edit/CKEditor.vue'
    import Uploader from 'components/Uploader.vue'

    export default {
        components: { CkEditor, Uploader },
        data: () => ({
            loading: false
        }),
        props: {
            model: {
                type: Object,
                twoWay: true,
                required: true
            },
            name: {
                type: String,
                required: true
            },
            baseURL: {
                type: String,
                required: true
            }
        },
        computed: {
            submitMethod () {
                return this.model.id ? 'patch' : 'post'
            },
            submitURL () {
                return this.model.id ? `${this.baseURL}${this.model.id}/` : `${this.baseURL}`
            },
            dataToSubmit () {
                let obj = _.cloneDeep(this.model)

                obj.attachments = _.map(this.model.attachments, file => file.id)

                return obj
            }
        },
        methods: {
            submit () {
                this.loading = true

                this.$http[this.submitMethod](this.submitURL, this.dataToSubmit)
                    .then(res => {
                        this.$emit('submitted', this, res.data)
                    }, res => {
                        if (res.status === 400) this.errors = res.data
                    })
                    .then(() => {
                        this.loading = false
                    })
            }
        }
    }
</script>