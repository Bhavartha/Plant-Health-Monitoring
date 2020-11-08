<template>
   <q-page class="flex justify-center text-center">
      <div class="q-mx-md">
         <h3>Plants recommender</h3>
         <p style="margin-top: -30px">
            Get recommendations on what new plants should you choose based on
            current plants that yield good result
         </p>
         <q-select
            filled
            label="Select multiple plants"
            v-model="selectedPlants"
            use-input
            use-chips
            multiple
            input-debounce="0"
            @new-value="createValue"
            :options="filterOptions"
            @filter="filterFn"
         />
         <q-slider
            v-model="count"
            markers
            :min="1"
            :max="10"
            label
            :label-value="'Recommend ' + count + ' plants'"
            label-always
            color="primary"
            class="q-mt-xl"
         />
         <q-btn
            no-caps
            color="primary"
            icon="psychology"
            label="Get recommendations"
            @click="onClick"
            class="q-my-lg"
            :disable="!selectedPlants || selectedPlants.length == 0"
         />
      </div>
      <q-dialog v-model="dataAvail" persistent>
         <plant-list @close="reset" :data="data" />
      </q-dialog>
   </q-page>
</template>

<script>
function initState() {
   return {
      selectedPlants: null,
      filterOptions: plantOptions,
      count: 5,
      data: null,
      dataAvail: false,
   };
}

const plantOptions = [
   "almond",
   "aloe vera",
   "apple",
   "apple gourd",
   "apricot",
   "avocados",
   "bamboo",
   "bananas",
   "banyan",
   "beans",
   "beetroot",
   "betelvine",
   "blackberries",
   "bottle gourd",
   "bougainvillea",
   "brinjal",
   "broccoli",
   "cabbage",
   "capsicum",
   "cardamom",
   "carrot",
   "cashew",
   "cherry",
   "chikoo",
   "chillies",
   "cinnamon",
   "clove",
   "cocoa",
   "coconut",
   "coffee",
   "coriander",
   "corn",
   "cotton",
   "cucumber",
   "custard apple",
   "dahlia",
   "dates",
   "fenugreek",
   "fox brush orchid",
   "frangipani",
   "ginger",
   "grape",
   "groundnut",
   "guava",
   "hibiscus",
   "jasmine",
   "jowar",
   "jute",
   "lemon",
   "lemongrass",
   "lettuce",
   "lichi",
   "maize",
   "mandarins",
   "mangoes",
   "maple",
   "marigold",
   "melon",
   "millets",
   "moong",
   "neem",
   "nutmeg",
   "okra",
   "onion",
   "orange",
   "pansy",
   "papaya",
   "peach",
   "peaches",
   "pear",
   "peas",
   "pepper",
   "pepper_bell",
   "pineapple",
   "plum",
   "pomegranate",
   "potato",
   "pumpkin",
   "radish",
   "raspberries",
   "rice",
   "rose",
   "silk",
   "sitafal",
   "soybean",
   "spinach",
   "strawberry",
   "sugarcane",
   "tea",
   "tomato",
   "tomatoes",
   "tulsi",
   "tur",
   "turmeric",
   "turnip",
   "urad",
   "walnut",
   "water melon",
   "wheat",
   "zinnia",
];

export default {
   components: {
      "plant-list": require("components/PlantsList").default,
   },
   data() {
      return initState();
   },
   methods: {
      reset() {
         Object.assign(this.$data, initialState());
      },
      createValue(val, done) {
         // Calling done(var) when new-value-mode is not set or is "add", or done(var, "add") adds "var" content to the model
         // and it resets the input textbox to empty string
         // ----
         // Calling done(var) when new-value-mode is "add-unique", or done(var, "add-unique") adds "var" content to the model
         // only if is not already set and it resets the input textbox to empty string
         // ----
         // Calling done(var) when new-value-mode is "toggle", or done(var, "toggle") toggles the model with "var" content
         // (adds to model if not already in the model, removes from model if already has it)
         // and it resets the input textbox to empty string
         // ----
         // If "var" content is undefined/null, then it doesn't tampers with the model
         // and only resets the input textbox to empty string

         if (val.length > 0) {
            const selectedPlants = (this.selectedPlants || []).slice();

            val.split(/[,;|]+/)
               .map((v) => v.trim())
               .filter((v) => v.length > 0)
               .forEach((v) => {
                  if (plantOptions.includes(v) === false) {
                     plantOptions.push(v);
                  }
                  if (selectedPlants.includes(v) === false) {
                     selectedPlants.push(v);
                  }
               });

            done(null);
            this.selectedPlants = selectedPlants;
         }
      },

      filterFn(val, update) {
         update(() => {
            if (val === "") {
               this.filterOptions = plantOptions;
            } else {
               const n = val.toLowerCase();
               this.filterOptions = plantOptions.filter(
                  (v) => v.toLowerCase().indexOf(n) > -1
               );
            }
         });
      },

      async onClick() {
         console.log(this.selectedPlants);
         const res = await this.$axios.post("http://localhost:5000/recommend", {
            data: this.selectedPlants,
            count: this.count,
         });
         this.data = res.data;
         this.dataAvail = true;
      },
   },
};
</script>
