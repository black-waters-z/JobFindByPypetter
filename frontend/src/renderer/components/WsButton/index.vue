<template>
    <button class="ws-button">
        <slot></slot>
    </button>
</template>

<script setup lang="ts">
</script>

<style scoped lang="scss">
.ws-button {
    border: none;
    padding: 10px 30px;
    border-radius: 100px;
    background-color: white;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-in-out;
    font-size: 19px;
    cursor: pointer;

    &:hover {
        background-color: #f5f5f5;
    }

    &:active {
        transform: scale(0.95);
    }
}
</style>