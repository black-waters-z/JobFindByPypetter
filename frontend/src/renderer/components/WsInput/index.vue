<template>
    <input class="ws-input" v-model="model" />
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
    modelValue: string;
}>();

const emit = defineEmits<{
    (e: "update:modelValue", value: string): void;
}>();

const model = computed({
    get: () => props.modelValue,
    set: (value: string) => emit("update:modelValue", value),
});
</script>

<style scoped lang="scss">
.ws-input {
    border: none;
    outline: none;
    background: white;
    font-size: 22px;
    padding: 10px 20px;
    margin: 20px 10px;
    border-radius: 10px;
}
</style>
