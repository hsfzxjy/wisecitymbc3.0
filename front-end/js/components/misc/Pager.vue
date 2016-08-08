<template>
    <div>
        <p class="text-xs-center">
            <slot name="no-results" v-if="!isLoading && isNoResults">
                空空如也～～
            </slot>
        </p>
        <p class="text-xs-center">
            <slot name="loading" v-if="isLoading">
                加载中...
            </slot>
        </p>
        <div class="pagination">
            <button 
                v-show="hasPrev" 
                :class="buttonClass"
                @click.stop="$emit('prev')">
                上一页
            </button>
            <button 
                v-show="hasNext" 
                :class="buttonClass"
                @click.stop="$emit('next')">
                下一页
            </button>
        </div>        
    </div>
</template>

<style scoped>
    p.text-xs-center {
        padding: .75rem 0;
    }

    div.pagination {
        text-align: center;
        display: block;
    }
</style>

<script>
    export default {
        props: {
            hasNext: {
                type: Boolean,
                default: true
            },
            hasPrev: {
                type: Boolean,
                default: true
            },
            isLoading: {
                type: Boolean,
                default: false
            },
            isNoResults: {
                type: Boolean,
                default: false
            }
        },
        computed: {
            buttonClass () {
                return [
                    !this.isLoading || 'disabled',
                    'btn',
                    'btn-primary'
                ]
            }
        }
    }
</script>