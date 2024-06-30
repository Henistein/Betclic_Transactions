document.getElementById('scrapeButton').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Execute the script on the current active tab
  const [profit] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: scrapePage,
  });

  const profit_display = document.getElementById('profitDisplay');
  profit_display.textContent = `Profit: ${profit.result.toFixed(2)}`
});


async function scrapePage() {
  const PaymentType = {
    DEPOSIT: "deposit",
    WITHDRAWAL: "withdrawal" 
  }

  async function clickTab(label) {
    const tab = Array.from(document.querySelectorAll('[data-qa="tab-btn"]'))
                    .find(tab => tab.querySelector('.tab_label').textContent.trim() === label);
    if (tab) {
        tab.click();
    } else {
        console.error(`Tab with label "${label}" not found.`);
    }
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  // Function to click the "Load More" button and wait for new items to load
  function clickLoadMoreButton() {
      return new Promise((resolve) => {
          const loadMoreButton = document.querySelector('button[data-qa="payment-history-load-more"]');
          if (loadMoreButton) {
              loadMoreButton.click();
              setTimeout(() => {
                  resolve(true); 
              }, 500);
          } else {
              resolve(false);  // No more "Load More" button found
          }
      });
  }


  function extract_transactions(type) {
    const history = document.querySelector('bc-payment-history-' + type);
    const amounts_contents = history.querySelectorAll('div.myAccount_boxTitleContent');
    const title_contents = history.querySelectorAll('div.myAccount_boxTitleEnd');

    const titles = [];
    const amounts = [];

    // Collect each transaction title ('Confirmado' or 'Recusado')
    title_contents.forEach(tit => {
      titles.push(tit.querySelector('span.tag_label').textContent);
    });

    // Filter just the confirmed amounts
    for (let i = 0; i < titles.length; i++) {
      if(titles[i] === "Confirmado"){
        amounts.push(parseFloat(amounts_contents[i].querySelector('span.myAccount_amount').textContent.replace(/[^\d,]/g, '').replace(',', '.')));
      }
    }

    return amounts;

  }


  await clickTab("Dep\u00F3sitos");
  await clickLoadMoreButton();
  let deposits = extract_transactions(PaymentType.DEPOSIT);

  await clickTab('Levantamentos');
  await clickLoadMoreButton();
  let withdrawals = extract_transactions(PaymentType.WITHDRAWAL);

  let profit = withdrawals.reduce((partialSum, a) => partialSum + a, 0) 
            - deposits.reduce((partialSum, a) => partialSum + a, 0);

  return profit;
}