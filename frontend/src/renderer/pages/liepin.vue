<template>
    <view class="liepin">
        <textarea v-model="liepinInputString" id="" style="width: 600px;height: 400px;"></textarea>
        <br>
        <WsButton @click="start">开始投递</WsButton>
        <WsButton @click="stop">停止投递</WsButton>
    </view>
</template>

<script setup lang="ts">
import WsButton from '@/components/WsButton/index.vue'
import { ref, computed } from 'vue';
const liepinInputStart = ref({
    "chrome_driver_path": "",
    "search_key": "",
    "start_page": 1,
    "page_size": 10
})

const liepinInputString = computed({
    get: () => JSON.stringify(liepinInputStart.value, null, 2), // 格式化为易读的 JSON
    set: (value) => {
        try {
            liepinInputStart.value = JSON.parse(value); // 反序列化为对象
        } catch (e) {
            console.error("无效的 JSON 输入");
        }
    }
});

async function start() {
    const result = fetch("http://127.0.0.1:8000/liepin/start", {
        method: "POST",
        body: JSON.stringify(liepinInputStart.value),
        headers: {
            "Content-Type": "application/json"
        }
    })
}

function stop() {
    console.log("stop")
    fetch("http://127.0.0.1:8000/liepin/stop", {
        method: "POST",
        body: JSON.stringify({
            "reason": "用户主动停止"
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
}

</script>