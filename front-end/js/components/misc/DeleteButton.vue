<template>
    <div @click="click">
        <slot></slot>
    </div>
</template>

<script>
    export default {
        props: {
            list: {
                type: Array,
                required: true,
                twoWay: true
            },
            index: {
                required: true
            },
            id: {
                required: true
            },
            baseURL: {
                type: String,
                required: true
            }
        },

        methods: {
            click () {
                this.$http.delete(`${this.baseURL}${this.id}/`)
                    .then(() => {
                        this.list.splice(this.index, 1)
                    })
            }
        }
    }
</script>