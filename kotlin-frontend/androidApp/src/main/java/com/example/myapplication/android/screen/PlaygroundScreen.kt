package com.example.myapplication.android.screen

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import com.example.myapplication.android.Buttons
import com.example.myapplication.android.NavigationGraph
import com.example.myapplication.android.api.ApiException
import com.example.myapplication.android.api.GameApi
import kotlinx.coroutines.launch
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min
import kotlin.math.roundToInt

enum class DragDirection { UP, DOWN, LEFT, RIGHT }

data object PlaygroundScreen : AppScreen("playground") {
    @Composable
    override fun Header(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Text(
            "Playground",
            style = MaterialTheme.typography.titleLarge
        )
    }

    @Composable
    override fun Body(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        var grid by remember { mutableStateOf(GameApi.getGame().getGrid()) }
        var moves by remember { mutableIntStateOf(GameApi.getGame().getMovesLeft()) }
        var score by remember { mutableIntStateOf(GameApi.getGame().getScore()) }

        // Check if no moves are left
        LaunchedEffect(moves) {
            if (moves == 0) {
                NavigationGraph.navigateTo(GameOverScreen)
            }
        }
        // Row for moves and score display
        Row(
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(16.dp)
        ) {
            // Update moves dynamically
            moves = GameApi.getGame().getMovesLeft()
            score = GameApi.getGame().getScore()
            Text(
                text = "Moves: $moves",
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.weight(1f),
                textAlign = TextAlign.Center
            )
            Text(
                text = "Score: $score",
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.weight(1f),
                textAlign = TextAlign.Center
            )
        }
        Spacer(modifier = Modifier.size(16.dp))
        // Playground grid
        TilesMatchPlayground(grid, setErrorOccurred, setErrorMessage) { updatedGrid ->
            grid = updatedGrid
        }
    }

    @Composable
    override fun Footer(setErrorOccurred: (Boolean) -> Unit, setErrorMessage: (String) -> Unit) {
        Buttons.PauseButton()
    }
}


@Composable
fun GridTile(
    color: Color,
    value: String,
    selected: Boolean,
    onClick: () -> Unit,
    onDrag: (DragDirection) -> Unit
) {

    // Animate the tile roundness based on the selected state
    val roundVal by animateDpAsState(
        targetValue = if (selected) 16.dp else 8.dp, label = ""
    )

    val colorInternal by animateColorAsState(
        targetValue = color, label = "", animationSpec = tween(500)
    )

    val tileSize = 50.dp / GameApi.getGame().getGrid().size * 6f

    val spacing = 8.dp / GameApi.getGame().getGrid().size * 6f

    val maxOffset = tileSize + spacing

    // Animate the tile offset based on the drag gesture
    val offsetX = remember { Animatable(0f) }
    val offsetY = remember { Animatable(0f) }
    val coroutineScope = rememberCoroutineScope()

    var dir: DragDirection?

    Box(
        modifier = Modifier
            .size(tileSize)
            .offset { IntOffset(offsetX.value.roundToInt(), offsetY.value.roundToInt()) }
            .background(colorInternal, shape = RoundedCornerShape(roundVal))
            // Handle tile click
            .clickable(onClick = {
                onClick()
            })
            // Handle tile drag
            .pointerInput(Unit) {
                detectDragGestures(
                    // While dragging, change the tile offset
                    onDrag = { change, dragAmount ->
                        coroutineScope.launch {
                            // Snap the tile offset to the drag amount
                            // Limit the offset to a maximum of tile size plus spacing
                            offsetX.snapTo(
                                max(
                                    min(offsetX.value + dragAmount.x, maxOffset.toPx()),
                                    -maxOffset.toPx()
                                )
                            )
                            offsetY.snapTo(
                                max(
                                    min(offsetY.value + dragAmount.y, maxOffset.toPx()),
                                    -maxOffset.toPx()
                                )
                            )
                            if (abs(dragAmount.x) > abs(dragAmount.y))
                                offsetY.snapTo(0f)
                            else
                                offsetX.snapTo(0f)
//                            println("offsetX: ${offsetX.value}, offsetY: ${offsetY.value}")
                        }
                        change.consume()
                    },
                    // When the drag ends, determine the direction and call the onDrag callback
                    onDragEnd = {

                        dir = when {
                            offsetX.value > 5 -> DragDirection.RIGHT
                            offsetX.value < -5 -> DragDirection.LEFT
                            offsetY.value > 5 -> DragDirection.DOWN
                            offsetY.value < -5 -> DragDirection.UP
                            else -> null
                        }

                        if (dir != null) {
                            onDrag(dir!!)
                        }

                        // Animate the updated tile offset back to the original position
                        coroutineScope.launch {
                            offsetX.animateTo(0f, tween(300))
                            offsetY.animateTo(0f, tween(300))
                        }
                    }
                )
            },
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text = value,
            style = MaterialTheme.typography.titleLarge
        )
    }
}

@Composable
fun TilesMatchPlayground(
    grid: List<List<GridElement>>,
    setErrorOccurred: (Boolean) -> Unit,
    setErrorMessage: (String) -> Unit,
    onGridUpdate: (List<List<GridElement>>) -> Unit
) {

    // State for the selected tile
    var selectedTile by remember { mutableStateOf<GridElement?>(null) }

    // Handler for tile tap
    fun tileTap(tile: GridElement) {
        if (tile.isBonus()) {
            GameApi.getGame().bonusMove(tile.x, tile.y)
            onGridUpdate(GameApi.getGame().getGrid())
            selectedTile = null
            return
        }
        if (tile == selectedTile) {
            selectedTile = null
            return
        }
        if (selectedTile == null) {
            selectedTile = tile
        } else {
            val x1 = selectedTile!!.x
            val y1 = selectedTile!!.y
            val x2 = tile.x
            val y2 = tile.y
            try {
                GameApi.getGame().makeMove(x1, y1, x2, y2)
            } catch (e: ApiException) {
                setErrorOccurred(true)
                setErrorMessage(e.message ?: "An error occurred")
            }
            onGridUpdate(GameApi.getGame().getGrid())
            selectedTile = null
        }
    }

    // Handler for tile drag
    fun swapTileWithDirection(tile: GridElement, direction: DragDirection) {
        val (x, y) = tile.x to tile.y

        // Determine target coordinates based on drag direction
        val targetX = when (direction) {
            DragDirection.LEFT -> x - 1
            DragDirection.RIGHT -> x + 1
            else -> x
        }
        val targetY = when (direction) {
            DragDirection.UP -> y - 1
            DragDirection.DOWN -> y + 1
            else -> y
        }

        // Check if target coordinates are within grid bounds
        if (targetX in grid.indices && targetY in grid[targetX].indices) {
            val targetTile = grid[targetY][targetX]
            try {
                GameApi.getGame().makeMove(x, y, targetTile.x, targetTile.y)
            } catch (e: ApiException) {
                setErrorOccurred(true)
                setErrorMessage(e.message ?: "An error occurred")
            }
            onGridUpdate(GameApi.getGame().getGrid()) // Update the grid after the move
        }
    }

    val spacing = 8.dp / GameApi.getGame().getGrid().size * 6f

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(spacing),
        modifier = Modifier
            .background(Color.LightGray, shape = RoundedCornerShape(spacing))
            .padding(spacing)
    ) {
        for (row in grid) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(spacing),
                verticalAlignment = Alignment.CenterVertically
            ) {
                for (tile in row) {
                    GridTile(
                        color = tile.getColor(),
                        value = tile.getValue(),
                        selected = selectedTile == tile,
                        onClick = { tileTap(tile) },
                        onDrag = { dir -> swapTileWithDirection(tile, dir) }
                    )
                }
            }
        }
    }
}

@Preview
@Composable
fun PlaygroundScreenPreview() {
    PlaygroundScreen.Content(true)
}
