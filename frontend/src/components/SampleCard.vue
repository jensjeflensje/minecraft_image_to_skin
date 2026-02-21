<template>
  <div class="card">
    <header class="card-title">{{ title }}</header>
    <div class="card-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string }>()
</script>

<style scoped>
.card {
  border-radius: 18px;
  padding: 1.6rem 1.8rem;
  background: #ffffffcc;
  backdrop-filter: blur(12px);
  box-shadow: 0 18px 40px rgba(20, 20, 20, 0.12);
  min-width: 600px;
}

.card-title {
  font-weight: 700;
  font-size: 1.2rem;
  margin-bottom: 0.75rem;
}

.card-content {
  color: #34332f;
}
</style>
