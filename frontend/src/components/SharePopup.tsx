import Button from './Button'

type SharePopupProps = {
  gameId: string
  onClose: () => void
}

function SharePopup({ gameId, onClose }: SharePopupProps) {
  const link = `${window.location.origin}/play/${gameId}`

  return (
    <div role="dialog" aria-label="Share game">
      <p>{link}</p>
      <Button onClick={() => navigator.clipboard.writeText(link)}>Copy</Button>
      <Button onClick={onClose}>Close</Button>
    </div>
  )
}

export default SharePopup
