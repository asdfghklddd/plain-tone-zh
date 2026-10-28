// Billing panel (synthetic sample, before)
export function Billing() {
  return (
    <Card>
      <h1>Billing</h1>
      <Text className="subtitle">Supercharge your workflow. Payments made simple.</Text>
      <Text className="description">This section lets you manage your plan and payment methods.</Text>
      <Text className="description">Here you can update your card details at any time.</Text>
      <Text className="helper">Click here to learn more about billing.</Text>
      <input type="text" placeholder="Card number" />
      <button onClick={openMenu}><MoreIcon /></button>
      <Button variant="primary">Pay now</Button>
      <Button variant="danger">Delete payment method</Button>
    </Card>
  );
}
