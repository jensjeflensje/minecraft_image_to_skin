import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    projectName: 'Image to Skin',
  }),
  actions: {},
})
