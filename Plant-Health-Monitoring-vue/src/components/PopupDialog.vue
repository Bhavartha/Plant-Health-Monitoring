<template>
   <q-card style="max-width:600px">
      <q-card-section>
         <div v-if="data.error" class="text-h5">Error</div>
         <div v-else class="text-h5">Result</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
         <div class="custom-alert">
            <span style="font-size: 18px">
               {{ data.msg }}
            </span>
            <q-img
               class="q-ml-xl"
               :src="getImg"
               style="width: 40px; height: 40px"
            />
         </div>
         <div v-if="!data.error" class="custom-alert q-mt-md">
            <span style="font-size: 16px">
               {{ data.treatment }}
            </span>
         </div>
      </q-card-section>
      <q-card-actions align="around">
         <q-btn flat label="OK" color="primary" v-close-popup @click="close" />
      </q-card-actions>
   </q-card>
</template>

<script>
export default {
   props: ["data"],
   methods: {
      close() {
         this.$emit("close");
      },
   },
   computed: {
      getImg() {
         if (this.data.msg == "Healthy")
            return "https://www.flaticon.com/svg/static/icons/svg/725/725105.svg";
         return "https://www.flaticon.com/svg/static/icons/svg/725/725099.svg";
      },
   },
};
</script>

<style lang="scss" scoped>
</style>