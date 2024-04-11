<script>
    import { onMount } from 'svelte';
    import { load } from './+page.js';
    let startDate = new Date().toISOString().split('T')[0]; // 시작일을 오늘로 설정합니다.
    const endDate = new Date().toISOString().split('T')[0]; // 종료일을 오늘로 고정합니다.
    let purchase_decided_list = [];
    let orderDetails = []; // 주문 상세 정보를 저장할 배열
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

    // 오늘의 날짜를 선택합니다.
    function selectToday() {
        startDate = new Date().toISOString().split('T')[0];
    }

    // 최근 3일을 선택합니다.
    function selectThreeDays() {
        startDate = new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    }

    // 최근 일주일을 선택합니다.
    function selectWeek() {
        startDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    }


    // 데이터를 가져오는 함수
    async function fetchData() {
        isLoading = true; // 로딩 시작
        try {
            // 날짜 형식이 맞지 않으면 alert를 띄우고 함수를 종료합니다.
            if (!startDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
                alert('날짜 형식이 맞지 않습니다. YYYY-MM-DD 형식으로 입력해 주세요.');
                return;
            }
            const datetime = `${startDate}T00:00:00`; // 날짜에 시간을 추가하여 ISO 8601 형식으로 만듭니다.
            const result = await load({ fetch: window.fetch }, datetime);
            purchase_decided_list = result.purchase_decided_list;
            orderDetails = result.order_details;
            console.log('orderDetails:', orderDetails);

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
        } catch (error) {
            console.error(error);
            alert('데이터를 불러오는 중 오류가 발생했습니다. 입력 값을 확인해 주세요.');
        } finally {
            isLoading = false; // 로딩 완료
        }   
    }

    // 컴포넌트가 마운트될 때 fetchData 함수를 호출합니다.
    onMount(fetchData);
</script>

<button on:click={selectToday}>오늘</button>
<button on:click={selectThreeDays}>최근 3일</button>
<button on:click={selectWeek}>일주일</button>
<p>
    시작일: <input type="date" bind:value={startDate} max={endDate}/>
    ~ 종료일: <input type="date" value={endDate} readonly />
    <button on:click={fetchData}>조회</button>
</p>

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

<!-- orderDetails를 사용하여 데이터를 테이블로 표시 -->
<table>
    <thead>
        <tr>
            <th>Product Order ID</th>
            <th>Product Order Status</th>
            <!-- 필요한 다른 헤더를 여기에 추가 -->
        </tr>
    </thead>
    <tbody>
        {#each orderDetails as item (item.productOrder.productOrderId)}
            <tr>
                <td>{item.productOrder.productOrderId}</td>
                <td>{item.productOrder.productOrderStatus}</td>
                <!-- 필요한 다른 데이터를 여기에 추가 -->
            </tr>
        {/each}
    </tbody>
</table>

<!-- purchase_decided_list를 사용하여 데이터를 표시
<ul>
    {#each purchase_decided_list as item (item.productOrderId)}
        <li>{item.productOrderId}: {item.productOrderStatus}</li>
    {/each}
</ul> -->

<style>
    /* Add any necessary styles here */
</style>