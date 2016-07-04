<template>
    <div>
        <textarea :id="editorId" cols="30" rows="10" v-model="model"></textarea>
    </div>
</template>

<script>
    import $script from 'scriptjs'

    export default {
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
            $script('//cdn.ckeditor.com/4.5.9/standard/ckeditor.js', () => {
                this.ckeditor = CKEDITOR.replace(this.editorId)
                this.ckeditor.on('change', () => {
                    this.model = this.ckeditor.getData()
                })
            })
        }
    }
</script>