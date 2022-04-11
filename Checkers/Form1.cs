using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Checkers
{
    public partial class Form1 : Form
    {
        const int mapSize = 8;
        const int cellSize = 50;

        int currentPlayer;

        Button prevButton;

        bool isMoving;

        int[,] map = new int [mapSize, mapSize];

        Image whiteFigure;
        Image blackFigure;

        public Form1()
        {
            InitializeComponent();

            whiteFigure = new Bitmap(new Bitmap(@"C:/Users/thepa/Desktop/Cours/ProjetFinal/Checkers/assets/whiteCheckers.png"), new Size(cellSize - 10, cellSize - 10));
            blackFigure = new Bitmap(new Bitmap(@"C:/Users/thepa/Desktop/Cours/ProjetFinal/Checkers/assets/blackCheckers.png"), new Size(cellSize - 10, cellSize - 10));

            this.Text = "Checkers";

            Init();
        }

        public void Init()
        {
            currentPlayer = 1;
            isMoving = false;
            prevButton = null;

            map = new int[mapSize,mapSize]{
                { 0,1,0,1,0,1,0,1},
                { 1,0,1,0,1,0,1,0},
                { 0,1,0,1,0,1,0,1},
                { 0,0,0,0,0,0,0,0},
                { 0,0,0,0,0,0,0,0},
                { 2,0,2,0,2,0,2,0},
                { 0,2,0,2,0,2,0,2},
                { 2,0,2,0,2,0,2,0},
            };

            CreateMap();
        }

        public void CreateMap()
        {
            this.Width = (mapSize+1) * cellSize;
            this.Height = (mapSize+1) * cellSize;

            for(int i = 0; i < mapSize; i++)
            {
                for (int j = 0; j < mapSize; j++)
                {
                    Button button = new Button();
                    button.Location = new Point(j * cellSize, i * cellSize);
                    button.Size = new Size(cellSize, cellSize);
                    button.Click += new EventHandler(OnFigurePress);
                    if (map[i, j] == 1)
                        button.Image = whiteFigure;
                    else if(map[i, j] == 2)button.Image = blackFigure;

                    if(i%2!=0)
                    {
                        if(j%2==0)
                        {
                            button.BackColor = Color.Gray;
                        }
                    }
                    if (i % 2 == 0)
                    {
                        if (j % 2 != 0)
                        {
                            button.BackColor = Color.Gray;
                        }
                    }
                    this.Controls.Add(button);
                }
            }
        }

        public void SwitchPlayer()
        {
            currentPlayer = currentPlayer == 1 ? 2 : 1;
        }

        public Color GetPrevButtonColor()
        {
            if ((prevButton.Location.Y/cellSize % 2) != 0)
            {
                if ((prevButton.Location.X/cellSize % 2) == 0)
                {
                    return Color.Gray;
                }
            }
            if ((prevButton.Location.Y/cellSize % 2) == 0)
            {
                if ((prevButton.Location.X/cellSize % 2) != 0)
                {
                    return Color.Gray;
                }
            }
            return Color.White;
        }

        public void OnFigurePress(object sender, EventArgs e)
        {
            if (prevButton != null)
                prevButton.BackColor = GetPrevButtonColor();

            Button pressedButton = sender as Button;

            if(map[pressedButton.Location.Y/cellSize, pressedButton.Location.X/cellSize] != 0 && map[pressedButton.Location.Y / cellSize, pressedButton.Location.X / cellSize] == currentPlayer)
            {
                pressedButton.BackColor = Color.Red;
                isMoving = true;
            }
            else
            {
                if(isMoving)
                {
                    int temp = map[pressedButton.Location.Y/cellSize, pressedButton.Location.X/ cellSize];
                    map[pressedButton.Location.Y / cellSize, pressedButton.Location.X / cellSize] = map[prevButton.Location.Y / cellSize, prevButton.Location.X / cellSize];
                    map[prevButton.Location.Y / cellSize, prevButton.Location.X / cellSize] = temp;
                    pressedButton.Image = prevButton.Image;
                    prevButton.Image = null;
                    isMoving=false;
                }
            }

            prevButton = pressedButton;
        }
    }
}
