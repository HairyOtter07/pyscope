<template>
    <div
        class="flex flex-row w-full items-center justify-between bg-slate-800/50 py-4 px-6 border-b-slate-400 border-b"
    >
        <img src="~/assets/images/name_logo.png" class="h-7" />
        <div class="flex flex-row-reverse gap-2">
            <div v-if="!dashboard">
                <p>Log In</p>
            </div>
            <div
                v-else-if="loading"
                class="bg-slate-700 w-52 rounded-lg animate-pulse"
            ></div>
            <p
                v-else
                class="peer hover:underline hover:cursor-pointer"
                @click="$emit('logOut')"
            >
                {{ userName }}
            </p>
            <p class="invisible peer-hover:visible text-slate-400">(Log Out)</p>
        </div>
    </div>
</template>
<script setup lang="ts">
defineProps<{
    dashboard: boolean;
    loading: boolean;
    userName?: string;
}>();
defineEmits(["logOut"]);
</script>
