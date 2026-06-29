<template>
    <div
        class="flex flex-row w-full items-center justify-between border-slate-400 border rounded-lg p-4"
        :class="complete ? 'bg-slate-800/50' : 'bg-slate-800'"
    >
        <div class="flex flex-col">
            <h2
                class="text-xl"
                :class="complete ? 'text-slate-300 line-through' : 'text-white'"
            >
                {{ title }}
            </h2>
            <p class="text-sm text-slate-300">{{ course }}</p>
            <p class="text-sm text-slate-300">{{ submissionStatus }}</p>
        </div>
        <div class="flex flex-col items-end">
            <p
                class="text-lg whitespace-nowrap"
                :class="complete ? 'text-slate-300' : 'text-white'"
            >
                {{
                    dueDate
                        ? `Due ${dayjs(dueDate).format(FORMAT_STRING)}`
                        : "No Due Date"
                }}
            </p>
            <p class="text-sm text-slate-300 whitespace-nowrap">
                {{
                    lateDueDate
                        ? `Late Due ${dayjs(lateDueDate).format(FORMAT_STRING)}`
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
    complete: boolean;
    dueDate?: dayjs.Dayjs;
    lateDueDate?: dayjs.Dayjs;
}>();

const FORMAT_STRING = "MM/DD/YYYY [at] hh:mmA";
</script>
