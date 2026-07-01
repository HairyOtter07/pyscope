<template>
    <div class="relative" ref="dropdownRef">
        <button
            @click="toggleDropdown"
            class="flex flex-row text-white pl-4 pr-3 py-1 border border-slate-400 rounded"
        >
            {{ model }}
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
            >
                <path d="M0 0h24v24H0z" fill="none" />
                <path fill="currentColor" d="m12 15l-5-5h10z" />
            </svg>
        </button>

        <div
            v-if="isOpen"
            class="flex flex-col items-start absolute top-full right-0 bg-slate-600 text-white border border-slate-400 py-2 mt-1 rounded"
        >
            <div
                v-for="option in options"
                @click="handleSelect(option)"
                class="px-4 py-1 w-full hover:cursor-pointer hover:bg-slate-800 whitespace-nowrap"
            >
                {{ option }}
            </div>
        </div>
    </div>
</template>

<script setup>
const model = defineModel();
const props = defineProps({
    options: Array,
});
import { ref, onMounted, onUnmounted } from "vue";

const isOpen = ref(false);
const dropdownRef = ref(null);
const selected = ref("Spring 2026");

const toggleDropdown = () => {
    isOpen.value = !isOpen.value;
};

const handleSelect = (option) => {
    model.value = option;
    isOpen.value = false; // Close menu after action
};

// Close the dropdown if clicked outside the element
const handleClickOutside = (event) => {
    if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
        isOpen.value = false;
    }
};

onMounted(() => document.addEventListener("click", handleClickOutside));
onUnmounted(() => document.removeEventListener("click", handleClickOutside));
</script>
