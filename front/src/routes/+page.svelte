<script>
    import { onMount } from 'svelte';
    import { load } from './+page.js';
    let date = new Date().toISOString().split('T')[0]; // 오늘의 날짜를 YYYY-MM-DD 형식으로 가져옵니다.
    let purchase_decided_list = [];
    let isLoading = false; // 로딩 상태를 나타내는 변수

    // LastChangedTypes의 영문 키와 한글명을 매핑하는 객체
    const LastChangedTypes = {
        'PAY_WAITING': '결제 대기',
        'PAYED': '결제 완료',
        'EXCHANGE_OPTION': '옵션 변경',
        'DELIVERY_ADDRESS_CHANGED': '배송지 변경',
        'GIFT_RECEIVED': '선물 수락',
        'CLAIM_REJECTED': '클레임 철회',
        'DISPATCHED': '발송 처리',
        'CLAIM_REQUESTED': '클레임 요청',
        'COLLECT_DONE': '수거 완료',
        'CLAIM_HOLDBACK_RELEASED': '클레임 보류 해제',
        'CLAIM_COMPLETED': '클레임 완료',
        'PURCHASE_DECIDED': '구매 확정',
        'HOPE_DELIVERY_INFO_CHANGED': '배송 희망일 변경',
        'CLAIM_REDELIVERING': '교환 재배송처리'
    };

    const ProductOrderStatuses = {
        'PAYMENT_WAITING' : '결제 대기',
        'PAYED' : '결제 완료',
        'DELIVERING' : '배송 중',
        'DELIVERED' : '배송 완료',
        'PURCHASE_DECIDED' : '구매 확정',
        'EXCHANGED' : '교환',
        'CANCELED' : '취소',
        'RETURNED' : '반품',
        'CANCELED_BY_NOPAYMENT' : '미결제 취소',
    };

        // 각 상태의 카운트를 저장하는 객체를 초기화합니다.
    let product_order_status_counts = Object.keys(ProductOrderStatuses).reduce((counts, status) => {
        counts[status] = 0;
        return counts;
    }, {});

    async function fetchData() {
        isLoading = true; // 로딩 시작
        const datetime = `${date}T00:00:00`; // 날짜에 시간을 추가하여 ISO 8601 형식으로 만듭니다.
        const result = await load({ fetch: window.fetch }, datetime);
        purchase_decided_list = result.purchase_decided_list;
        isLoading = false; // 로딩 완료

        // 카운트를 초기화합니다.
        product_order_status_counts = Object.keys(ProductOrderStatuses).reduce((counts, status) => {
            counts[status] = 0;
            return counts;
        }, {});

        // 각 상태의 카운트를 계산합니다.
        product_order_status_counts = purchase_decided_list.reduce((counts, item) => {
            counts[item.productOrderStatus]++;
            return counts;
        }, product_order_status_counts);
    }
    
    // 컴포넌트가 마운트될 때 fetchData 함수를 호출합니다.
    onMount(fetchData);
</script>

<input type="date" bind:value={date} />
<button on:click={fetchData}>Fetch Data</button>

<!-- 로딩 아이콘을 조건적으로 표시 -->
{#if isLoading}
    <div>Loading...</div>
{/if}


<!-- 각 상태의 카운트를 표시 -->
<ul>
    {#each Object.entries(product_order_status_counts) as [status, count]}
        <li>{ProductOrderStatuses[status]}: {count}건</li>
    {/each}
</ul>

<!-- purchase_decided_list를 사용하여 데이터를 표시 -->
<ul>
    {#each purchase_decided_list as item (item.productOrderId)}
        <li>{item.productOrderId}: {item.productOrderStatus}</li>
    {/each}
</ul>

<style>
    /* Add any necessary styles here */
</style>