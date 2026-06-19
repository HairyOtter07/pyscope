<template>
    <div
        class="flex flex-row w-full items-center justify-between bg-slate-800 border-slate-400 border rounded-lg p-4"
    >
        <div class="flex flex-col">
            <h2 class="text-xl text-white">{{ title }}</h2>
            <p class="text-sm text-slate-200">{{ course }}</p>
            <p class="text-sm text-slate-200">{{ submissionStatus }}</p>
        </div>
        <div class="flex flex-col items-end">
            <p class="text-lg text-white">
                {{
                    dueDate
                        ? dayjs(dueDate).format(FORMAT_STRING)
                        : "No Due Date"
                }}
            </p>
            <p class="text-sm text-slate-200">
                {{
                    lateDueDate
                        ? dayjs(lateDueDate).format(FORMAT_STRING)
                        : "No Late Due Date"
                }}
            </p>
        </div>
    </div>
</template>
<script setup lang="ts">
import dayjs from "dayjs";
defineProps<{
    title: string;
    course: string;
    submissionStatus: string;
    dueDate?: dayjs.Dayjs;
    lateDueDate?: dayjs.Dayjs;
}>();

const FORMAT_STRING = "dddd, MMMM DD, YYYY [at] hh:mmA";
</script>
