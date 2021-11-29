const List = {
    data() {
        return {
            listData: [],
            completeItems: [],
            incompleteItems: [],
            totalCosts: 0.0,
            costPerUser: 0.0,
        }
    },
    mounted() {
        //get request
        //use results
        let url = '/json/list/' + window.listId;
        let numMembers = window.numMembers;
        axios.get(url)
            .then(function (response) {
                // handle success
                listApp.listData = response.data;
                console.log("data");
                console.log(response.data);
                for (item of listApp.listData){
                    if (item['complete']){
                        listApp.completeItems.push(item)
                        if (item['price']){
                            listApp.totalCosts += parseFloat(item['price'])
                        }
                    }
                    else {
                        listApp.incompleteItems.push(item)
                    }
                }
                listApp.totalCosts = listApp.totalCosts.toFixed(2)
                listApp.costPerUser = (listApp.totalCosts / numMembers).toFixed(2);

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
                    if (item['complete']){
                        completeItems.push(item);
                        if (item['price']){
                            totalCosts += parseFloat(item['price']);
                        }
                    }
                    else {
                        incompleteItems.push(item);
                    }
                }

                listApp.completeItems = completeItems;
                listApp.incompleteItems = incompleteItems;
                listApp.totalCosts = totalCosts.toFixed(2);
                listApp.costPerUser = (listApp.totalCosts / numMembers).toFixed(2);


            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        }, 10000);

    }

}

listApp = Vue.createApp(List).mount('#list');
