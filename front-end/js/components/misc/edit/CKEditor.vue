<template>
    <div>
        <textarea :id="editorId" cols="30" rows="10" v-model="model"></textarea>
    </div>
</template>

<style>
    .cke_top.cke_reset_all {
        height: 31px!important;
        overflow: auto;
    }
</style>

<script>
    import $script from 'scriptjs'

    export default {
        events: {
            ['CKEditor:insert-data']: function (data) {
                let ckeditor = CKEDITOR.instances[this.editorId]

                ckeditor.insertHtml(data)
            },
            ['CKEditor:reset']: function () {
                let ckeditor = CKEDITOR.instances[this.editorId]

                ckeditor.setData('')
            }
        },
        props: {
            editorId: {
                type: String,
                required: true
            },
            model: {
                type: String,
                required: true
            }
        },
        ready () {
            if (window.CKEDITOR)
                this.initEditor()
            else
                $script('//cdn.ckeditor.com/4.5.9/standard/ckeditor.js', this.initEditor.bind(this))
        },
        methods: {
            initEditor () {
                let ckeditor = CKEDITOR.replace(this.editorId, {
                    language: 'zh-CN',
                    removeButtons: 'Source,PasteFromWord,PasteText,Paste,Scayt,Superscript,Subscript,About,Anchor',
                    toolbarGroups: [
                        { name: 'styles', groups: [ 'styles' ] },
                        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
                        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
                        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
                        { name: 'links', groups: [ 'links' ] },
                        { name: 'insert', groups: [ 'insert' ] },
                        { name: 'forms', groups: [ 'forms' ] },
                        { name: 'tools', groups: [ 'tools' ] },
                        { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
                        { name: 'others', groups: [ 'others' ] },
                        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
                        { name: 'colors', groups: [ 'colors' ] },
                        { name: 'about', groups: [ 'about' ] }
                    ],
                    removePlugins: 'elementspath',
                    resize_enabled: false
                })
                ckeditor.on('change', () => {
                    this.model = ckeditor.getData()
                })
            }
        }
    }
</script>