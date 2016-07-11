<template>
    <vs-list-group flush>
        <vs-list-group-item v-for="file in model">
            {{ file.file_name }}
            <a
                href="#"
                v-if="deleteLink"
                class="pull-xs-right"
                @click.stop.prevent="removeFile($index)">
                删除
            </a>
            <a
                href="{{file.storage_url}}"
                class="pull-xs-right"
                target="_blank">
                下载
            </a>
        </vs-list-group-item>
        <slot></slot>
    </vs-list-group>
</template>

<style scoped>
    li a {
        margin: 0 .2rem;
    }
</style>

<script>
    export default {
        props: {
            model: {
                type: Array,
                required: true,
                twoWay: true
            },
            baseURL: {
                type: String,
                required: false
            },
            deleteLink: {
                type: Boolean,
                default: false
            }
        },
        methods: {
            removeFile (index) {
                console.log(this.model[index].id)
                let id = this.model[index].id

                this.$http.delete(`${this.baseURL}${id}/`)
                    .then(() => {
                        this.model.splice(index, 1)
                    })
            }
        }
    }
</script>