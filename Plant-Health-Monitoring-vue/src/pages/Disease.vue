<template>
   <q-page class="flex flex-center text-center">
      <div class="q-mx-md">
         <div class="file-upload-form">
            <h3 class="mobile-hide">Is your plant healthy?</h3>
            <h4 class="mobile-only">Is your plant healthy?</h4>
            <p style="margin-top: -30px">Do a quick test here to find out</p>
            <br />
            <br />
            <div class="relative-position">
               <q-select
                  class="absolute-center"
                  filled
                  v-model="plantType"
                  use-input
                  input-debounce="0"
                  label="Choose plant type"
                  :options="options"
                  @filter="filterFn"
                  style="width: 250px"
                  behavior="menu"
               >
                  <template v-slot:no-option>
                     <q-item>
                        <q-item-section class="text-grey">
                           No results
                        </q-item-section>
                     </q-item>
                  </template>
               </q-select>
            </div>
            <label class="custom-file-upload q-mt-xl">
               Choose File
               <input type="file" @change="previewImage" accept="image/*"
            /></label>
         </div>
         <q-btn
            color="primary"
            icon="psychology"
            label="predict"
            @click="onClick"
            class="q-my-lg"
            :disable="!imageData || !plantType"
         />
         <div class="image-preview q-mt-lg" v-if="imageData.length > 0">
            <q-img
               id="image"
               :src="imageData"
               spinner-color="white"
               style="height: auto; max-width: 350px"
            />
         </div>
      </div>
      <q-dialog v-model="dataAvail" persistent>
         <popup-dialog @close="reset" :data="data" />
      </q-dialog>
   </q-page>
</template>

<script>
const plantOptions = [
   "Apple",
   "Cherry",
   "Corn",
   "Grape",
   "Peach",
   "Pepper Bell",
   "Potato",
   "Strawberry",
];

// Takes a data URI and returns the Data URI corresponding to the resized image at the wanted size.
function resizedataURL(datas, wantedWidth, wantedHeight) {
   return new Promise(async function (resolve, reject) {
      // We create an image to receive the Data URI
      var img = document.createElement("img");

      // When the event "onload" is triggered we can resize the image.
      img.onload = function () {
         // We create a canvas and get its context.
         var canvas = document.createElement("canvas");
         var ctx = canvas.getContext("2d");

         // We set the dimensions at the wanted size.
         canvas.width = wantedWidth;
         canvas.height = wantedHeight;

         // We resize the image with the canvas method drawImage();
         ctx.drawImage(this, 0, 0, wantedWidth, wantedHeight);

         var dataURI = canvas.toDataURL();

         // This is the return of the Promise
         resolve(dataURI);
      };

      // We put the Data URI in the image's src attribute
      img.src = datas;
   });
}

function initialState() {
   return {
      imageData: "",
      plantType: null,
      plantOptions,
      options: plantOptions,
      data: null,
      dataAvail: false,
   };
}

export default {
   components: {
      "popup-dialog": require("components/PopupDialog").default,
   },
   data() {
      return initialState();
   },
   methods: {
      reset() {
         Object.assign(this.$data, initialState());
      },
      async onClick() {
         var newDataUri = await resizedataURL(this.imageData, 28, 28);
         console.log(newDataUri);
         const payload = {
            img: newDataUri,
            plant: this.plantType,
         };
         console.log(payload);
         const res = await this.$axios.post(
            "http://localhost:5000/d_detector",
            payload
         );
         this.data = res.data;
         this.dataAvail = true;
      },
      filterFn(val, update) {
         if (val === "") {
            update(() => {
               this.options = plantOptions;
            });
            return;
         }
         update(() => {
            const p = val.toLowerCase();
            this.options = plantOptions.filter(
               (v) => v.toLowerCase().indexOf(p) > -1
            );
         });
      },
      previewImage: function (event) {
         // Reference to the DOM input element
         var input = event.target;
         // Ensure that you have a file before attempting to read it
         if (input.files && input.files[0]) {
            // create a new FileReader to read this image and convert to base64 format
            var reader = new FileReader();
            // Define a callback function to run, when FileReader finishes its job
            reader.onload = (e) => {
               // Note: arrow function used here, so that "this.imageData" refers to the imageData of Vue component
               // Read image as base64 and set to imageData
               this.imageData = e.target.result;
            };
            // Start the reader job - read file as a data url (base64 format)
            reader.readAsDataURL(input.files[0]);
         }
      },
   },
};
</script>

<style lang="scss" scoped>
input[type="file"] {
   display: none;
}

.custom-file-upload {
   display: inline-block;
   padding: 8px 30px;
   cursor: pointer;
   background: $primary;
   color: whitesmoke;
   font-weight: 500;
   font-size: 1.1rem;
   border-radius: 7px;
   &:focus {
      outline: none;
   }
}
</style>