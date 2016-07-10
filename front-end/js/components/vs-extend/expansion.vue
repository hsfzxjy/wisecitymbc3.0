<template>
    <vs-collapse-toggle 
        :target="id">
        <slot name="title">
            <a href="javascript:void 0" style="display: block;">{{ title }}</a>
        </slot>
    </vs-collapse-toggle>
    <vs-collapse
        :id="id">
        <slot name="content"></slot>
    </vs-collapse>
</template>

<script>
    import { StrUtils } from 'utils/index.es'

    export default {
        computed: {
            id () {
                return StrUtils.randStr()
            }
        },
        props: {
            title: {
                type: String,
                default: ''
            }
        },
        events: {
            ['toggled::collapse'] ({id}) {
                if (id === this.id) {
                    this.$dispatch('toggled')
                }

                return true
            }
        }
    }
</script>