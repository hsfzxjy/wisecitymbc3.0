<template>
    <div>
        <vs-form @submit.prevent="submit" class="col-md-8 sm-no-padding" :errors="errors">
            <slot name="fields-before"></slot>
            <fieldset class="form-group">
                <ck-editor :editor-id="name+'-editor'" :model.sync="model.content"></ck-editor>
            </fieldset>
            <slot name="fields-after"></slot>
        </vs-form>
        <div class="col-md-4 sm-no-padding">
            <div class="col-xs-6 col-md-12 sm-no-padding">
                <uploader
                    @file-uploaded="insertFileToEditor"
                    :upload-status.sync="uploadStatus"
                    :browse-button-id="name+'-editor-upload'"
                    :files="model.attachments">
                    <vs-buttons
                        block
                        id="{{name}}-editor-upload"
                        variant="primary"
                        :disabled="uploadStatus.uploading || loading">
                        添加文件
                    </vs-buttons>
                </uploader>
            </div>
            <div class="col-xs-6 col-md-12 sm-no-padding">
                <vs-buttons :disabled="loading" @click="submit" block>
                    <slot name="submit-name">发布</slot>
                </vs-buttons>
            </div>
            <div class="col-xs-12 sm-no-padding">
                <vs-progress
                    v-show="uploadStatus.uploading"
                    variant="success"
                    :value="uploadStatus.percent"
                    striped>
                </vs-progress>
                <vs-list-group>
                    <vs-list-group-item
                        v-for="file in model.attachments">
                        <a
                            href="javascript: void 0"
                            @click.stop="insertFileToEditor(model.attachments[$index])">
                            {{ file.file_name }}
                        </a>
                        <a
                            href="javascript:void 0"
                            class="pull-xs-right"
                            @click.stop="removeFile($index)">
                            删除
                        </a>
                    </vs-list-group-item>
                </vs-list-group>
            </div>
        </div>
    </div>
</template>

<script>
    import { files } from 'consts.es'
    import { clearObject } from 'utils/index.es'
    import CkEditor from 'misc/edit/CKEditor.vue'
    import Uploader from 'misc/Uploader.vue'

    export default {
        components: { CkEditor, Uploader },
        data: () => ({
            loading: false,
            errors: {},
            uploadStatus: {
                uploading: false,
                percent: 0
            }
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
            baseUrl: {
                type: String,
                required: true
            }
        },
        computed: {
            submitMethod () {
                return this.model.id ? 'patch' : 'post'
            },
            submitURL () {
                return this.model.id ? `${this.baseUrl}${this.model.id}/` : `${this.baseUrl}`
            },
            dataToSubmit () {
                let obj = _.cloneDeep(this.model)

                obj.attachments = _.map(this.model.attachments, file => file.id)

                return obj
            }
        },
        methods: {
            submit () {
                this.$http[this.submitMethod](this.submitURL, this.dataToSubmit)
                    .then(res => {
                        this.$emit('submitted', this, res.data)
                        clearObject(this.model)
                        this.$broadcast('CKEditor:reset')
                    })
            },
            removeFile (index) {
                this.model.attachments.splice(index, 1)
            },
            insertFileToEditor (file) {
                let html
                console.log(file)
                if (file.file_type === files.FileType.image) {
                    html = `<img src="${file.storage_url}"  title="${file.file_name}" />`
                } else {
                    html = `<a href="${file.storage_url}">${file.file_name}</a>`
                }

                console.log(html)

                this.$broadcast('CKEditor:insert-data', html)
            }
        }
    }
</script>
