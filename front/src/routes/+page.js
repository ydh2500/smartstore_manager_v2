export const load = async ({ fetch }, datetime) => {
    const url = `http://127.0.0.1:8000/api/order/all_changed_list?since_from=${encodeURIComponent(datetime)}`;
    const response = await fetch(url, {
        mode: 'cors', // CORS 요청을 보냅니다.
    });
    const text = await response.text();
    console.log(text); // 응답 출력
    try {
        return { 
            purchase_decided_list: JSON.parse(text)['lastChangeStatus_list'],
        };
    } catch (error) {
        console.error('Parsing error:', error);
        throw error;
    }
}