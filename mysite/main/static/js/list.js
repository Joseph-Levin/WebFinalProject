const List = {
    data() {
        return {
            listData: [],
            completeItems: [],
            incompleteItems: [],
        }
    },
    mounted() {
        //get request
        //use results
        let url = '/json/list/' + window.listId
        axios.get(url)
            .then(function (response) {
                // handle success
                listApp.listData = response.data;
                for (item of listApp.listData){
                    if (item.fields['complete']){
                        listApp.completeItems.push(item)
                    }
                    else {
                        listApp.incompleteItems.push(item)
                    }
                }

                console.log(response.data);
                console.log(listApp.completeItems)
                console.log(listApp.incompleteItems)
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        setInterval(()=>{
            axios.get(url)
            .then(function (response) {
                // handle success
                listApp.listData = response.data;
                let completeItems = [];
                let incompleteItems = [];
                for (item of listApp.listData){
                    if (item.fields['complete']){
                        completeItems.push(item);
                    }
                    else {
                        incompleteItems.push(item);
                    }
                }

                listApp.completeItems = completeItems;
                listApp.incompleteItems = incompleteItems;

            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        }, 10000);

    }

}

listApp = Vue.createApp(List).mount('#list');