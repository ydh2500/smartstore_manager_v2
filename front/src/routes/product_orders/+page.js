export const load = async ({ fetch }, product_order_ids) => {
    const url = `http://127.0.0.1:8000/api/order/order_detail_list?product_order_ids=${product_order_ids.join(',')}`;
    const response = await fetch(url, {
        mode: 'cors', // CORS 요청을 보냅니다.
    });
    const text = await response.text();
    console.log(text); // 응답 출력
    try {
        return { 
            order_detail_list: JSON.parse(text)['order_detail_list'],
        };
    } catch (error) {
        console.error('Parsing error:', error);
        throw error;
    }
}