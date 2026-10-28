// Billing panel (synthetic sample, after)
export function Billing() {
  return (
    <Card>
      <h1>Billing</h1>
      <label htmlFor="card">Card number</label>
      <input id="card" type="text" inputMode="numeric" />
      <button aria-label="More options" onClick={openMenu}><MoreIcon /></button>
      <p>Pro plan, $29 per month. Your card ending 4821 will be charged $29 today.</p>
      <Button variant="primary">Pay $29</Button>
      <p>Removing this card cancels auto-renewal; your plan ends on Nov 30.</p>
      <Button variant="danger">Delete card ending 4821</Button>
    </Card>
  );
}
