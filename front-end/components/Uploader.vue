<template>
    <slot></slot>
</template>

<script>
    import _ from 'lodash'

    function getUploader (options) {
        return (new QiniuJsSDK()).uploader(options)
    }

    export default {
        props: {
            browseButtonId: {
                type: String,
                required: true
            },
            fileAddUrl: {
                type: String,
                coerce (value) {
                    return value || '/api/files/'
                }
            },
            files: {
                type: Array,
                required: true
            }
        },
        ready () {
            getUploader(this.getOptions())
        },
        methods: {
            getOptions () {
                let options = {
                    browse_button: this.browseButtonId,
                    uptoken_url: '/api/uptoken/',
                    runtimes: 'html5,flash,html4',
                    domain: '7xkade.dl1.z0.glb.clouddn.com',
                    auto_start: true
                }

                let init = {
                    Key (up, file) {
                        return `${Date.now()}/${file.name}`
                    },
                    FileUploaded: (up, file, info) => {
                        let key = JSON.parse(info).key

                        this.$http.post(this.fileAddUrl, { path: key })
                            .then((res) => {
                                let file = res.data

                                this.files.push(file)
                                this.$emit('file-uploaded', file)
                            })
                    }
                }

                _.forEach("FilesAdded BeforeUpload UploadProgress Error UploadComplete".split(' '), (eventName) => {
                    init[eventName] = () => {
                        let args = [_.kebabCase(eventName)].concat(Array.prototype.slice.call(arguments))

                        this.$emit.apply(this, args)
                    }
                })

                options.init = init

                return options
            }
        }
    }
</script>