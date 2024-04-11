export const load = async ({ fetch }, datetime) => {
    const url = `http://127.0.0.1:8000/api/order/all_changed_list?since_from=${encodeURIComponent(datetime)}`;
    const response = await fetch(url, {
        mode: 'cors', // CORS 요청을 보냅니다.
    });
    const text = await response.text();
    const order_detail_list = [];
    console.log('text:', text); // 응답 출력
    // lastChangeStatus_list키가 없으면
    if (!JSON.parse(text)['lastChangeStatus_list']) {
        return { 
            purchase_decided_list: [],
        };
    }
    // 키가 있는 경우엔
    else {
        const product_order_ids = JSON.parse(text)['lastChangeStatus_list'].map((item) => item['productOrderId']);
        console.log('product_order_ids: ',product_order_ids);
        const details = await load_details({ fetch }, product_order_ids);
        console.log('details: ',details);
        const order_detail_list = await details['order_detail_list'];
        console.log('order_detail_list: ',order_detail_list);
    }

    try {
        return { 
            purchase_decided_list: JSON.parse(text)['lastChangeStatus_list'],
            order_details: order_detail_list,
        };
    } catch (error) {
        console.error('Parsing error in load:', error);
        throw error;
    }
}


async function load_details ({ fetch }, product_order_ids) {
    const url = `http://127.0.0.1:8000/api/order/order_detail_list?product_order_ids=${product_order_ids.join(',')}`;
    console.log(url);
    const response = await fetch(url, {
        mode: 'cors', // CORS 요청을 보냅니다.
    });
    const text = await response.text();
    console.log(text); // 응답 출력
    try {
        return { 
            order_detail_list: JSON.parse(text)['data'],
        };
    } catch (error) {
        console.error('Parsing error in load details:', error);
        throw error;
    }
}