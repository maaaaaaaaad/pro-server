import {
  Body,
  Controller,
  Delete,
  Get,
  Patch,
  Post,
  Query,
  UploadedFile,
  UseGuards,
  UseInterceptors,
} from '@nestjs/common'
import { ItemService } from './item.service'
import { JwtAuthGuard } from '../auth/jwt/jwt-auth.guard'
import {
  ApiBearerAuth,
  ApiBody,
  ApiConsumes,
  ApiOperation,
  ApiQuery,
  ApiTags,
} from '@nestjs/swagger'
import { User } from '../common/decorators/user.decorator'
import { UserEntity } from '../auth/entities/user.entity'
import {
  ItemRegisterInputDto,
  ItemRegisterOutputDto,
} from './dtos/item.register.dto'
import { FileInterceptor } from '@nestjs/platform-express'
import { multerOptions } from '../common/utils/multer.options'
import { CategoriesGetOutputDto } from './dtos/categories.get.dto'
import { ItemsGetInputDto } from './dtos/items.get.dto'
import { ItemUpdateInputDto } from './dtos/item.update.dto'
import { ItemDeleteInputDto } from './dtos/item.delete.dto'
import { ItemGetInputDto } from './dtos/item.get.dto'

@Controller('item')
@ApiTags('item')
export class ItemController {
  constructor(private readonly itemService: ItemService) {}

  @UseGuards(JwtAuthGuard)
  @Post()
  @UseInterceptors(
    FileInterceptor('coverImage', multerOptions('item-cover-image')),
  )
  @ApiConsumes('multipart/form-data')
  @ApiBearerAuth('access-token')
  @ApiOperation({
    summary: 'Register user item',
  })
  @ApiBody({
    type: ItemRegisterInputDto,
  })
  async register(
    @User() user: UserEntity,
    @UploadedFile() image: Express.Multer.File,
    @Body() itemRegisterInputDto: ItemRegisterInputDto,
  ): Promise<ItemRegisterOutputDto> {
    const path = `http://localhost:${process.env.PORT}/media/item-cover-image/${image.filename}`
    if (image) {
      itemRegisterInputDto.coverImage = path
    }
    return await this.itemService.register(user, itemRegisterInputDto)
  }

  @UseGuards(JwtAuthGuard)
  @Patch()
  @ApiConsumes('application/x-www-form-urlencoded')
  @ApiOperation({ summary: 'Update user item' })
  @ApiBody({ type: ItemUpdateInputDto })
  @ApiBearerAuth('access-token')
  async update(
    @Body() itemUpdateInputDto: ItemUpdateInputDto,
    @User() owner: UserEntity,
  ) {
    return await this.itemService.update(itemUpdateInputDto, owner)
  }

  @UseGuards(JwtAuthGuard)
  @Delete()
  @ApiConsumes('application/x-www-form-urlencoded')
  @ApiOperation({ summary: 'Delete user item' })
  @ApiBearerAuth('access-token')
  @ApiQuery({ name: 'pk', type: ItemDeleteInputDto, required: true })
  async delete(
    @Query('pk') itemDeleteInputDto: ItemDeleteInputDto,
    @User() user: UserEntity,
  ) {
    return await this.itemService.delete(itemDeleteInputDto, user)
  }

  @Get('all')
  @ApiOperation({
    summary: 'Get items',
  })
  async items(@Query() itemsGetInputDto: ItemsGetInputDto) {
    return await this.itemService.items(itemsGetInputDto)
  }

  @Get('one')
  @ApiOperation({ summary: 'Get item' })
  async item(@Query() itemGetInputDto: ItemGetInputDto) {
    return await this.itemService.item(itemGetInputDto)
  }

  @Get('categories')
  @ApiOperation({
    summary: 'Get categories',
  })
  async categories(): Promise<CategoriesGetOutputDto> {
    return await this.itemService.categories()
  }
}
