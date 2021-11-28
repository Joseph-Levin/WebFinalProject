const List = {
    data() {
        return {
            listData: [],
            completeItems: [],
            incompleteItems: [],
            totalCosts: 0.0,
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
                        if (item.fields['price']){
                            listApp.totalCosts += parseFloat(item.fields['price'])
                        }
                    }
                    else {
                        listApp.incompleteItems.push(item)
                    }
                }
                listApp.totalCosts = listApp.totalCosts.toFixed(2)
                console.log(listApp.totalCosts);

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
                let totalCosts = 0.0
                for (item of listApp.listData){
                    if (item.fields['complete']){
                        completeItems.push(item);
                        if (item.fields['price']){
                            totalCosts += parseFloat(item.fields['price']);
                        }
                    }
                    else {
                        incompleteItems.push(item);
                    }
                }

                listApp.completeItems = completeItems;
                listApp.incompleteItems = incompleteItems;
                listApp.totalCosts = totalCosts.toFixed(2);
                console.log(listApp.totalCosts);

            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        }, 10000);

    }

}

listApp = Vue.createApp(List).mount('#list');
