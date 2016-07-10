<template>
    <slot></slot>
</template>

<script>
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
            },
            uploadStatus: {
                type: Object,
                twoWay: true,
                default: {
                    uploading: false,
                    percent: 0
                }
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
                                this.$dispatch('file-uploaded', file)
                            }).then(() => {
                                this.uploadStatus.uploading = false
                            })
                    },
                    UploadProgress: (up, progress) => {
                        this.uploadStatus.percent = progress.percent
                        this.$dispatch('upload-progress', up, progress)
                    },
                    BeforeUpload: (up, file) => {
                        this.uploadStatus = {
                            uploading: true,
                            percent: 0
                        }
                        this.$dispatch('before-upload', up, file)
                    }
                }

                _.forEach("FilesAdded Error UploadComplete".split(' '), (eventName) => {
                    init[eventName] = function () {
                        let args = [_.kebabCase(eventName)].concat(Array.prototype.slice.call(arguments))

                        this.$dispatch.apply(this, args)
                    }.bind(this)
                })

                options.init = init

                return options
            }
        }
    }
</script>