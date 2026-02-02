from samvidai.layout.layoutlm import segment_layout

def test_layout_segmentation_returns_blocks():
    images = ["page1.png", "page2.png"]
    blocks = segment_layout(images)

    assert isinstance(blocks, list)
    assert len(blocks) > 0
    assert "clause_id" in blocks[0]
    assert "text" in blocks[0]